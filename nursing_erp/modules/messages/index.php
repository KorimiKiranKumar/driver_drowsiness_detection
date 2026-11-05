<?php
$pageTitle = "Communication Hub";
require_once '../../includes/header.php';
$db = getDB();
?>

<div class="space-y-8 animate-fade-in max-w-5xl mx-auto">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
            <h1 class="text-3xl font-extrabold text-primary tracking-tight">Messaging Hub</h1>
            <p class="text-gray-500 mt-1 font-medium">Broadcast announcements and personalized SMS notifications to parents and staff.</p>
        </div>
        <div class="flex gap-3">
            <span class="bg-pink-100 text-pink-600 px-4 py-2 rounded-xl text-xs font-black uppercase tracking-widest flex items-center gap-2">
                <i class="fas fa-coins"></i> Balance: 12,450
            </span>
        </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- New Message Form -->
        <div class="bg-white rounded-[40px] border border-gray-100 shadow-sm overflow-hidden">
            <div class="p-8 bg-gray-50/50 border-b border-gray-100 flex items-center gap-4">
                <div class="w-10 h-10 bg-pink-500 rounded-xl flex items-center justify-center text-white text-lg">
                    <i class="fas fa-paper-plane"></i>
                </div>
                <h3 class="text-xl font-black text-primary">Compose Broadcast</h3>
            </div>
            <form class="p-8 space-y-6">
                <div class="space-y-2">
                    <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest">Target Audience *</label>
                    <select class="w-full px-5 py-3 bg-gray-50 border border-gray-100 rounded-2xl outline-none focus:border-accent text-xs font-bold text-gray-500">
                        <option>All Students & Parents</option>
                        <option>B.Sc Nursing (4th Year)</option>
                        <option>Faculty Members</option>
                        <option>Transport Users</option>
                    </select>
                </div>
                <div class="space-y-2">
                    <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest">Message Template</label>
                    <select class="w-full px-5 py-3 bg-gray-50 border border-gray-100 rounded-2xl outline-none focus:border-accent text-xs font-bold text-gray-500">
                        <option>General Announcement</option>
                        <option>Fee Due Reminder</option>
                        <option>Attendance Warning</option>
                        <option>Holiday Notice</option>
                    </select>
                </div>
                <div class="space-y-2">
                    <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest">Message Content *</label>
                    <textarea rows="5" class="w-full px-5 py-3 bg-gray-50 border border-gray-100 rounded-2xl outline-none focus:border-accent text-xs font-bold" placeholder="Type institutional announcement here..."></textarea>
                    <p class="text-[10px] text-right font-bold text-gray-400 uppercase">Characters: 0 / 160 (1 SMS)</p>
                </div>
                <button type="submit" class="w-full py-4 bg-pink-500 text-white rounded-[20px] font-black text-sm shadow-2xl shadow-pink-500/30 hover:scale-[1.02] transition-all flex items-center justify-center gap-3">
                    <i class="fas fa-broadcast-tower"></i> Send SMS Broadcast
                </button>
            </form>
        </div>

        <!-- Recent Broadcasts -->
        <div class="bg-white rounded-[40px] border border-gray-100 shadow-sm overflow-hidden flex flex-col">
            <div class="p-8 border-b border-gray-50 flex items-center justify-between">
                <h3 class="text-xl font-black text-primary">Transmission History</h3>
                <button class="text-gray-400 hover:text-primary"><i class="fas fa-ellipsis-v"></i></button>
            </div>
            <div class="flex-1 p-8 space-y-6 overflow-y-auto max-h-[500px] custom-scrollbar">
                <?php for($i=1; $i<=4; $i++): ?>
                <div class="p-5 bg-gray-50 rounded-3xl border border-gray-100 relative group transition-all hover:bg-white hover:shadow-xl">
                    <div class="flex items-center justify-between mb-3">
                        <span class="px-3 py-1 bg-erp_green/10 text-erp_green text-[10px] font-black rounded-full uppercase">Delivered</span>
                        <span class="text-[10px] font-bold text-gray-400 uppercase"><?php echo date('M d, H:i'); ?></span>
                    </div>
                    <p class="text-xs font-bold text-primary leading-relaxed mb-3">Dear Parent, this is a reminder regarding the pending tuition fee for the academic year 2024-25. Please clear before 15th June.</p>
                    <div class="flex items-center gap-2">
                        <div class="w-6 h-6 rounded-full bg-gray-200 flex items-center justify-center text-[8px] font-black text-gray-500">
                            AO
                        </div>
                        <span class="text-[10px] font-black text-gray-400 uppercase">By Admin Officer</span>
                    </div>
                </div>
                <?php endfor; ?>
            </div>
        </div>
    </div>
</div>

<?php require_once '../../includes/footer.php'; ?>
