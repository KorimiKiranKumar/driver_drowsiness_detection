<?php
$pageTitle = "Certificate Issuance Hub";
require_once '../../includes/header.php';
$db = getDB();
$courses = $db->query("SELECT * FROM courses")->fetchAll();
?>

<div class="space-y-8 animate-fade-in">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
            <h1 class="text-3xl font-extrabold text-primary tracking-tight">Institutional Certificates</h1>
            <p class="text-gray-500 mt-1 font-medium">Issue digital Bonafide, Transfer, and Course Completion certificates.</p>
        </div>
        <div class="flex gap-3">
            <button class="bg-primary text-white px-6 py-2.5 rounded-xl font-bold text-sm shadow-lg shadow-primary/30 hover:scale-105 transition-all flex items-center gap-2">
                <i class="fas fa-history"></i> Issuance History
            </button>
        </div>
    </div>

    <!-- Filter Section -->
    <div class="bg-white p-8 rounded-[40px] border border-gray-100 shadow-sm">
        <form class="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div class="space-y-2">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest">Select Course</label>
                <select class="w-full px-5 py-3 bg-gray-50 border border-gray-100 rounded-2xl outline-none focus:border-accent text-xs font-bold text-gray-500">
                    <?php foreach($courses as $c): ?>
                        <option value="<?php echo $c['id']; ?>"><?php echo $c['course_name']; ?></option>
                    <?php endforeach; ?>
                </select>
            </div>
            <div class="space-y-2">
                <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest">Certificate Type</label>
                <select class="w-full px-5 py-3 bg-gray-50 border border-gray-100 rounded-2xl outline-none focus:border-accent text-xs font-bold text-gray-500">
                    <option>Bonafide Certificate</option>
                    <option>Transfer Certificate (TC)</option>
                    <option>Course Completion</option>
                    <option>Fee Paid Certificate</option>
                </select>
            </div>
            <div class="md:col-span-2 flex items-end gap-3">
                <div class="flex-1 relative group">
                    <i class="fas fa-search absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
                    <input type="text" placeholder="Search student by name or ID..." class="w-full pl-12 pr-4 py-3 bg-gray-50 border border-gray-100 rounded-2xl outline-none focus:border-accent text-xs font-bold">
                </div>
                <button type="submit" class="bg-accent text-white px-8 py-3 rounded-2xl font-bold text-sm shadow-lg shadow-accent/20 transition-all">
                    LOAD
                </button>
            </div>
        </form>
    </div>

    <!-- Eligible Students -->
    <div class="bg-white rounded-[40px] border border-gray-100 shadow-sm overflow-hidden">
        <div class="p-8 border-b border-gray-50">
            <h3 class="text-xl font-black text-primary">Eligible Candidate Registry</h3>
        </div>
        <div class="overflow-x-auto">
            <table class="w-full text-left">
                <thead class="bg-gray-50/50">
                    <tr>
                        <th class="px-8 py-4 text-[10px] font-black text-gray-400 uppercase tracking-widest">Student Name</th>
                        <th class="px-8 py-4 text-[10px] font-black text-gray-400 uppercase tracking-widest">Admission No</th>
                        <th class="px-8 py-4 text-[10px] font-black text-gray-400 uppercase tracking-widest">Course Group</th>
                        <th class="px-8 py-4 text-[10px] font-black text-gray-400 uppercase tracking-widest text-right">Actions</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-gray-50">
                    <?php 
                    $demo_students = [
                        ['name' => 'Kiran Kumar', 'id' => 'HF/2024/001', 'course' => 'B.Sc Nursing'],
                        ['name' => 'Anjali Devi', 'id' => 'HF/2024/005', 'course' => 'GNM']
                    ];
                    foreach($demo_students as $s): ?>
                    <tr class="hover:bg-gray-50 transition-colors">
                        <td class="px-8 py-5 text-sm font-black text-primary uppercase"><?php echo $s['name']; ?></td>
                        <td class="px-8 py-5 text-xs font-bold text-gray-500"><?php echo $s['id']; ?></td>
                        <td class="px-8 py-5 text-xs font-bold text-gray-600 uppercase"><?php echo $s['course']; ?></td>
                        <td class="px-8 py-5 text-right">
                            <button class="px-4 py-2 bg-accent text-white text-[10px] font-black rounded-lg hover:bg-accent/80 transition-all uppercase tracking-widest shadow-lg shadow-accent/20">
                                Issue Certificate
                            </button>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>

<?php require_once '../../includes/footer.php'; ?>
