<?php
$pageTitle = "Institutional Staff Registry";
require_once '../../includes/header.php';
$db = getDB();
$staff_list = [
    ['name' => 'Dr. Ramesh Rao', 'id' => 'STF001', 'dept' => 'Nursing Foundation', 'desig' => 'Principal', 'phone' => '9876543210'],
    ['name' => 'Mrs. Sunita Verma', 'id' => 'STF005', 'dept' => 'Anatomy', 'desig' => 'Associate Professor', 'phone' => '8765432109'],
    ['name' => 'Mr. Amit Gupta', 'id' => 'STF012', 'dept' => 'Accounts', 'desig' => 'Admin Head', 'phone' => '7654321098']
];
?>

<div class="space-y-8 animate-fade-in">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
            <h1 class="text-3xl font-extrabold text-primary tracking-tight">Staff & Faculty Registry</h1>
            <p class="text-gray-500 mt-1 font-medium">Manage employee records, payroll profiles, and departmental assignments.</p>
        </div>
        <div class="flex gap-3">
            <button class="bg-primary text-white px-6 py-2.5 rounded-xl font-bold text-sm shadow-lg shadow-primary/30 hover:scale-105 transition-all flex items-center gap-2">
                <i class="fas fa-plus"></i> Add New Employee
            </button>
        </div>
    </div>

    <!-- Staff List -->
    <div class="bg-white rounded-[40px] border border-gray-100 shadow-sm overflow-hidden">
        <div class="p-8 border-b border-gray-50 flex items-center justify-between">
            <h3 class="text-xl font-black text-primary">Departmental Inventory</h3>
            <div class="flex gap-3">
                <select class="bg-gray-50 text-[10px] font-black text-gray-400 px-4 py-2 rounded-xl border-none outline-none uppercase tracking-widest">
                    <option>All Departments</option>
                    <option>Faculty</option>
                    <option>Administration</option>
                </select>
            </div>
        </div>
        <div class="overflow-x-auto">
            <table class="w-full text-left">
                <thead class="bg-gray-50/50">
                    <tr>
                        <th class="px-8 py-4 text-[10px] font-black text-gray-400 uppercase tracking-widest">Staff Name / ID</th>
                        <th class="px-8 py-4 text-[10px] font-black text-gray-400 uppercase tracking-widest">Department</th>
                        <th class="px-8 py-4 text-[10px] font-black text-gray-400 uppercase tracking-widest">Designation</th>
                        <th class="px-8 py-4 text-[10px] font-black text-gray-400 uppercase tracking-widest">Contact</th>
                        <th class="px-8 py-4 text-[10px] font-black text-gray-400 uppercase tracking-widest text-right">Actions</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-gray-50">
                    <?php foreach($staff_list as $s): ?>
                    <tr class="hover:bg-gray-50 transition-colors group">
                        <td class="px-8 py-5">
                            <div class="flex items-center gap-4">
                                <div class="w-10 h-10 bg-primary/10 text-primary rounded-xl flex items-center justify-center font-black text-xs">
                                    <?php echo substr($s['name'], 0, 1); ?>
                                </div>
                                <div>
                                    <p class="text-sm font-black text-primary uppercase"><?php echo $s['name']; ?></p>
                                    <p class="text-[10px] text-gray-400 font-bold tracking-widest"><?php echo $s['id']; ?></p>
                                </div>
                            </div>
                        </td>
                        <td class="px-8 py-5 text-xs font-bold text-gray-600 uppercase tracking-wide"><?php echo $s['dept']; ?></td>
                        <td class="px-8 py-5">
                            <span class="px-3 py-1 bg-accent/10 text-accent text-[10px] font-black rounded-full uppercase"><?php echo $s['desig']; ?></span>
                        </td>
                        <td class="px-8 py-5 text-sm font-medium text-gray-500"><?php echo $s['phone']; ?></td>
                        <td class="px-8 py-5 text-right">
                            <div class="flex justify-end gap-2 opacity-0 group-hover:opacity-100 transition-all">
                                <button class="w-8 h-8 flex items-center justify-center bg-accent/10 text-accent rounded-lg hover:bg-accent hover:text-white transition-all"><i class="fas fa-eye text-xs"></i></button>
                                <button class="w-8 h-8 flex items-center justify-center bg-erp_blue/10 text-erp_blue rounded-lg hover:bg-erp_blue hover:text-white transition-all"><i class="fas fa-edit text-xs"></i></button>
                            </div>
                        </td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</div>

<?php require_once '../../includes/footer.php'; ?>
