/**
 * Professional Driver Monitoring System - Frontend Module
 * Optimized for real-time performance and stable detection using MediaPipe landmarks.
 */

class DetectionMonitor {
    constructor(sessionId) {
        this.sessionId = sessionId;
        this.isMonitoring = false;
        this.frameNumber = 0;
        this.startTime = null;
        this.lastFrameTime = 0;
        this.fps = 0;
        this.processingCanvas = document.createElement('canvas');
        this.processingCanvas.width = 640;
        this.processingCanvas.height = 480;
        this.processingCtx = this.processingCanvas.getContext('2d', { alpha: false });

        // Rendering & Processing State
        this.isProcessing = false;
        this.alertActive = false;
        this.landmarks = null;
        this.currentState = "READY";

        // Web Audio API for Alarm
        this.audioCtx = null;
        this.oscillator = null;
        this.gainNode = null;
        this.alarmInterval = null;

        // Pose History Tracking
        this.poseHistory = {
            'STRAIGHT': 0,
            'UP': 0,
            'DOWN': 0,
            'LEFT': 0,
            'RIGHT': 0
        };

        // DOM Elements
        this.canvas = document.getElementById('videoFeed');
        this.ctx = this.canvas ? this.canvas.getContext('2d', { alpha: false }) : null;
        this.statusBadge = document.getElementById('statusBadge');
        this.alertOverlay = document.getElementById('alertOverlay');

        // Metrics Elements
        this.earValue = document.getElementById('earValue');
        this.marValue = document.getElementById('marValue');
        this.headPoseValue = document.getElementById('headPoseValue');
        this.drowsinessLevel = document.getElementById('drowsinessLevel');
        this.fpsCounter = document.getElementById('totalFrames');
        this.totalBlinks = document.getElementById('totalDrowsy');
        this.totalAlerts = document.getElementById('totalAlerts');
        this.sessionTimer = document.getElementById('cameraStatus');

        // Progress Bars
        this.earProgress = document.getElementById('earProgress');
        this.marProgress = document.getElementById('marProgress');

        // Pose History Elements
        this.poseElements = {
            'STRAIGHT': document.getElementById('countCenter'),
            'UP': document.getElementById('countUp'),
            'DOWN': document.getElementById('countDown'),
            'LEFT': document.getElementById('countLeft'),
            'RIGHT': document.getElementById('countRight')
        };

        // Buttons
        this.startBtn = document.getElementById('startBtn');
        this.stopBtn = document.getElementById('stopBtn');

        // Hidden Processing Video
        this.video = document.createElement('video');
        this.video.autoplay = true;
        this.video.playsInline = true;
        this.video.muted = true;
        this.video.style.display = 'none';
        document.body.appendChild(this.video);

        this.init();
    }

    init() {
        if (this.startBtn) this.startBtn.addEventListener('click', () => this.start());
        if (this.stopBtn) this.stopBtn.addEventListener('click', () => this.stop());
        window.addEventListener('beforeunload', () => this.stop());
    }

    async start() {
        if (this.isMonitoring) return;

        try {
            const constraints = {
                video: {
                    width: { ideal: 640, max: 640 },
                    height: { ideal: 480, max: 480 },
                    frameRate: { ideal: 24, max: 24 },
                    facingMode: "user"
                },
                audio: false
            };

            const stream = await navigator.mediaDevices.getUserMedia(constraints);
            this.video.srcObject = stream;

            if (!this.audioCtx) {
                this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            }

            this.isMonitoring = true;
            this.startTime = Date.now();
            this.updateButtonStates(true);

            this.renderLoop();
            this.processLoop();
            this.updateTimer();

        } catch (err) {
            console.error("Camera Access Error:", err);
            alert("Please enable camera access to use the monitoring system.");
        }
    }

    stop() {
        if (!this.isMonitoring) return;

        this.isMonitoring = false;
        this.stopAlarm();

        if (this.video.srcObject) {
            this.video.srcObject.getTracks().forEach(track => track.stop());
        }

        this.updateButtonStates(false);

        fetch('/detection/stop/', {
            method: 'POST',
            headers: { 'X-CSRFToken': this.getCsrfToken() }
        }).then(() => {
            window.location.href = '/detection/results/';
        });
    }

    updateButtonStates(active) {
        if (this.startBtn) this.startBtn.disabled = active;
        if (this.stopBtn) this.stopBtn.disabled = !active;
        if (this.statusBadge) {
            this.statusBadge.textContent = active ? "MONITORING ACTIVE" : "READY";
            this.statusBadge.className = `status-badge ${active ? 'status-normal' : ''}`;
        }
    }

    // --- RENDERING LOOP ---
    renderLoop(time) {
        if (!this.isMonitoring) return;

        if (time) {
            const delta = (time - this.lastFrameTime) / 1000;
            this.lastFrameTime = time;
            this.fps = Math.round(1 / delta);
            if (this.fpsCounter) this.fpsCounter.textContent = this.fps;
        }

        if (this.video.readyState === this.video.HAVE_ENOUGH_DATA) {
            this.ctx.save();
            this.ctx.scale(-1, 1);
            this.ctx.drawImage(this.video, -this.canvas.width, 0, this.canvas.width, this.canvas.height);
            this.ctx.restore();

            this.drawDetectionOverlay();
        }

        requestAnimationFrame((t) => this.renderLoop(t));
    }

    drawDetectionOverlay() {
        if (!this.landmarks || this.landmarks.length === 0) return;

        const color = this.currentState.includes('Drowsy') ? '#ff4b2b' :
            (this.currentState.includes('Blink') ? '#ffb347' : '#00d2ff');

        this.ctx.shadowBlur = 5;
        this.ctx.shadowColor = color;

        const mirrorX = (x) => this.canvas.width - x;

        // Draw all landmarks as small points (Subtle Face Mesh)
        this.ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
        Object.values(this.landmarks).forEach(([x, y]) => {
            this.ctx.beginPath();
            this.ctx.arc(mirrorX(x), y, 1, 0, 2 * Math.PI);
            this.ctx.fill();
        });

        // Landmark Indices for Features
        const LEFT_EYE = [362, 385, 387, 263, 373, 380];
        const RIGHT_EYE = [33, 160, 158, 133, 153, 144];
        const MOUTH = [13, 14, 78, 308];

        this.drawIndices(LEFT_EYE, '#00d2ff');
        this.drawIndices(RIGHT_EYE, '#00d2ff');
        this.drawIndices(MOUTH, '#ffb347');

        // Status Text Overlay
        this.ctx.fillStyle = color;
        this.ctx.font = "bold 24px Outfit";
        this.ctx.textAlign = "center";
        this.ctx.fillText(this.currentState.toUpperCase(), this.canvas.width / 2, 40);

        this.ctx.shadowBlur = 0;
    }

    drawIndices(indices, color) {
        this.ctx.strokeStyle = color;
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        indices.forEach((idx, i) => {
            const point = this.landmarks[idx];
            if (!point) return;
            const [x, y] = point;
            const mx = this.canvas.width - x;
            if (i === 0) this.ctx.moveTo(mx, y);
            else this.ctx.lineTo(mx, y);
        });
        this.ctx.closePath();
        this.ctx.stroke();
    }

    // --- PROCESSING LOOP (DETECTION) ---
    async processLoop() {
        if (!this.isMonitoring || this.isProcessing) return;

        this.isProcessing = true;

        try {
            const frame = this.captureFrame();

            const response = await fetch('/detection/detect/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify({ image: frame })
            });

            if (response.ok) {
                const data = await response.json();
                if (data.error) {
                    console.error("Server Error:", data.status);
                    if (this.statusBadge) this.statusBadge.textContent = "SERVER ERROR";
                } else {
                    this.updateUI(data);
                    this.landmarks = data.landmarks;
                    this.currentState = data.status;
                }
            }
        } catch (err) {
            console.error("Processing Error:", err);
            if (this.statusBadge) this.statusBadge.textContent = "CONNECTION ERROR";
        } finally {
            this.isProcessing = false;
            // Keep the server inference rate predictable. Rendering continues at
            // display refresh rate, so a slower inference cycle never freezes UI.
            if (this.isMonitoring) setTimeout(() => this.processLoop(), 100);
        }
    }

    captureFrame() {
        this.processingCtx.drawImage(this.video, 0, 0, this.processingCanvas.width, this.processingCanvas.height);
        return this.processingCanvas.toDataURL('image/jpeg', 0.6);
    }

    updateUI(data) {
        if (this.statusBadge) {
            this.statusBadge.textContent = data.status;
            this.statusBadge.className = `status-badge ${data.is_drowsy ? 'status-high' : (data.status.includes('Blink') ? 'status-medium' : 'status-normal')}`;
        }

        const updateVal = (el, val, suffix = '', animate = false) => {
            if (el && el.textContent !== val.toString()) {
                el.textContent = val + suffix;
                if (animate) {
                    el.classList.add('animate-pulse');
                    setTimeout(() => el.classList.remove('animate-pulse'), 500);
                }
            }
        };

        updateVal(this.earValue, (data.ear || 0).toFixed(3));
        updateVal(this.marValue, (data.mar || 0).toFixed(3));
        updateVal(this.headPoseValue, data.head_pose || "STRAIGHT");

        const currentPose = (data.head_pose || "STRAIGHT").toUpperCase();
        if (data.pose_history) {
            this.poseHistory = data.pose_history;
            Object.keys(this.poseElements).forEach(pose => {
                const el = this.poseElements[pose];
                if (el) {
                    updateVal(el, this.poseHistory[pose] || 0, '', pose === currentPose);
                    if (pose === currentPose) {
                        el.parentElement.style.opacity = '1';
                        el.parentElement.style.borderColor = 'var(--primary)';
                        el.parentElement.style.background = 'rgba(0, 242, 255, 0.15)';
                        el.parentElement.style.boxShadow = '0 0 10px var(--primary-glow)';
                    } else {
                        el.parentElement.style.opacity = '0.5';
                        el.parentElement.style.borderColor = 'rgba(255, 255, 255, 0.08)';
                        el.parentElement.style.background = 'transparent';
                        el.parentElement.style.boxShadow = 'none';
                    }
                }
            });
        }

        if (this.earProgress) {
            this.earProgress.style.width = `${Math.min((data.ear || 0) * 250, 100)}%`;
        }
        if (this.marProgress) {
            this.marProgress.style.width = `${Math.min((data.mar || 0) * 300, 100)}%`;
        }

        updateVal(this.totalBlinks, data.blink_count || 0, '', true);
        updateVal(this.totalAlerts, data.alert_count || 0, '', true);

        if (this.sessionTimer && this.startTime) {
            const elapsed = Math.floor((Date.now() - this.startTime) / 1000);
            const mins = Math.floor(elapsed / 60).toString().padStart(2, '0');
            const secs = (elapsed % 60).toString().padStart(2, '0');
            this.sessionTimer.textContent = `SESSION: ${mins}:${secs} | LINK ACTIVE`;
        }

        if (data.is_drowsy) {
            this.startAlarm();
            this.showAlertOverlay(true);
            if (this.drowsinessLevel) {
                this.drowsinessLevel.textContent = "CRITICAL";
                this.drowsinessLevel.className = "text-danger fw-bold text-glow";
            }
        } else {
            this.stopAlarm();
            this.showAlertOverlay(false);
            if (this.drowsinessLevel) {
                this.drowsinessLevel.textContent = data.status.includes('Blink') ? "WARNING" : "VIGILANT";
                this.drowsinessLevel.className = data.status.includes('Blink') ? "text-warning fw-bold" : "text-success fw-bold";
            }
        }
    }

    startAlarm() {
        if (this.alertActive) return;
        this.alertActive = true;

        if (this.audioCtx && this.audioCtx.state === 'suspended') {
            this.audioCtx.resume();
        }

        const playTone = () => {
            if (!this.alertActive) return;
            
            const osc = this.audioCtx.createOscillator();
            const gain = this.audioCtx.createGain();
            
            osc.type = 'square';
            osc.frequency.setValueAtTime(880, this.audioCtx.currentTime); // A5
            osc.frequency.exponentialRampToValueAtTime(440, this.audioCtx.currentTime + 0.1); // A4
            
            gain.gain.setValueAtTime(0, this.audioCtx.currentTime);
            gain.gain.linearRampToValueAtTime(0.3, this.audioCtx.currentTime + 0.05);
            gain.gain.linearRampToValueAtTime(0, this.audioCtx.currentTime + 0.2);
            
            osc.connect(gain);
            gain.connect(this.audioCtx.destination);
            
            osc.start();
            osc.stop(this.audioCtx.currentTime + 0.2);
        };

        playTone();
        this.alarmInterval = setInterval(playTone, 400);
    }

    stopAlarm() {
        if (!this.alertActive) return;
        this.alertActive = false;
        if (this.alarmInterval) {
            clearInterval(this.alarmInterval);
            this.alarmInterval = null;
        }
    }

    showAlertOverlay(show) {
        if (this.alertOverlay) {
            if (show) this.alertOverlay.classList.add('show');
            else this.alertOverlay.classList.remove('show');
        }
    }

    updateTimer() {
        if (!this.isMonitoring) return;
        const elapsed = Math.floor((Date.now() - this.startTime) / 1000);
        const mins = Math.floor(elapsed / 60).toString().padStart(2, '0');
        const secs = (elapsed % 60).toString().padStart(2, '0');
        if (this.sessionTimer) this.sessionTimer.textContent = `Session: ${mins}:${secs}`;
        setTimeout(() => this.updateTimer(), 1000);
    }

    getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
            document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1];
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.monitor = new DetectionMonitor(Date.now());
});
