<?php
$pageTitle = "Transport Fleet Management";
require_once '../../includes/header.php';
$db = getDB();
$routes = [
    ['name' => 'Route 01 (City Central)', 'bus' => 'TS09-EA-1234', 'driver' => 'Somu', 'count' => 42],
    ['name' => 'Route 02 (Eastern Suburbs)', 'bus' => 'TS09-EA-5678', 'driver' => 'Ravi', 'count' => 38],
    ['name' => 'Route 03 (North Bypass)', 'bus' => 'TS09-EA-9012', 'driver' => 'Gopi', 'count' => 25]
];
?>

<div class="space-y-8 animate-fade-in">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
            <h1 class="text-3xl font-extrabold text-primary tracking-tight">Institutional Fleet Control</h1>
            <p class="text-gray-500 mt-1 font-medium">Manage transport routes, vehicle allocations, and student mapping.</p>
        </div>
        <div class="flex gap-3">
            <button class="bg-primary text-white px-6 py-2.5 rounded-xl font-bold text-sm shadow-lg shadow-primary/30 hover:scale-105 transition-all flex items-center gap-2">
                <i class="fas fa-plus"></i> New Route
            </button>
        </div>
    </div>

    <!-- Summary Stats -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm flex items-center gap-4">
            <div class="w-12 h-12 bg-erp_blue/10 text-erp_blue rounded-2xl flex items-center justify-center text-xl">
                <i class="fas fa-bus"></i>
            </div>
            <div>
                <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest">Active Fleet</p>
                <h3 class="text-xl font-black text-primary">12 Vehicles</h3>
            </div>
        </div>
        <div class="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm flex items-center gap-4">
            <div class="w-12 h-12 bg-erp_green/10 text-erp_green rounded-2xl flex items-center justify-center text-xl">
                <i class="fas fa-users"></i>
            </div>
            <div>
                <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest">Total Users</p>
                <h3 class="text-xl font-black text-primary">456 Students</h3>
            </div>
        </div>
        <div class="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm flex items-center gap-4">
            <div class="w-12 h-12 bg-orange-100 text-orange-500 rounded-2xl flex items-center justify-center text-xl">
                <i class="fas fa-route"></i>
            </div>
            <div>
                <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest">Active Routes</p>
                <h3 class="text-xl font-black text-primary">08 Routes</h3>
            </div>
        </div>
    </div>

    <!-- Routes Table -->
    <div class="bg-white rounded-[40px] border border-gray-100 shadow-sm overflow-hidden">
        <div class="p-8 border-b border-gray-50 flex items-center justify-between">
            <h3 class="text-xl font-black text-primary">Operational Route Registry</h3>
            <button class="text-xs font-black text-accent uppercase tracking-widest hover:underline">Route Mapping</button>
        </div>
        <div class="overflow-x-auto">
            <table class="w-full text-left">
                <thead class="bg-gray-50/50">
                    <tr>
                        <th class="px-8 py-4 text-[10px] font-black text-gray-400 uppercase tracking-widest">Route Detail</th>
                        <th class="px-8 py-4 text-[10px] font-black text-gray-400 uppercase tracking-widest">Vehicle No</th>
                        <th class="px-8 py-4 text-[10px] font-black text-gray-400 uppercase tracking-widest">Driver</th>
                        <th class="px-8 py-4 text-[10px] font-black text-gray-400 uppercase tracking-widest text-center">Users</th>
                        <th class="px-8 py-4 text-[10px] font-black text-gray-400 uppercase tracking-widest text-right">Actions</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-gray-50">
                    <?php foreach($routes as $r): ?>
                    <tr class="hover:bg-gray-50 transition-colors group">
                        <td class="px-8 py-5 text-sm font-black text-primary uppercase"><?php echo $r['name']; ?></td>
                        <td class="px-8 py-5 text-xs font-bold text-gray-600"><?php echo $r['bus']; ?></td>
                        <td class="px-8 py-5 text-xs font-bold text-gray-500 uppercase"><?php echo $r['driver']; ?></td>
                        <td class="px-8 py-5 text-center">
                            <span class="px-3 py-1 bg-erp_blue/10 text-erp_blue text-[10px] font-black rounded-full uppercase"><?php echo $r['count']; ?> Students</span>
                        </td>
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
