<?php
$pageTitle = "Fee Collection Hub";
require_once '../../includes/header.php';
$db = getDB();

// Fetch Students for Search
$students = $db->query("SELECT id, admission_no, first_name, last_name FROM students WHERE is_deleted = 0 ORDER BY first_name ASC")->fetchAll();
$categories = $db->query("SELECT * FROM fee_categories")->fetchAll();
?>

<div class="space-y-8 animate-fade-in max-w-5xl mx-auto">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
            <h1 class="text-3xl font-extrabold text-primary tracking-tight">Institutional Fee Collection</h1>
            <p class="text-gray-500 mt-1 font-medium">Generate digital receipts and record student financial transactions.</p>
        </div>
        <a href="index.php" class="text-gray-400 hover:text-primary font-bold text-sm flex items-center gap-2">
            <i class="fas fa-arrow-left"></i> Back to Finance Hub
        </a>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Collection Form -->
        <div class="lg:col-span-2 space-y-8">
            <form action="../../api/finance/collect_fee.php" method="POST" class="bg-white rounded-[40px] border border-gray-100 shadow-sm overflow-hidden">
                <div class="p-8 bg-gray-50/50 border-b border-gray-100 flex items-center gap-4">
                    <div class="w-10 h-10 bg-erp_green rounded-xl flex items-center justify-center text-white text-lg">
                        <i class="fas fa-file-invoice"></i>
                    </div>
                    <h3 class="text-xl font-black text-primary">New Receipt Details</h3>
                </div>
                <div class="p-8 space-y-6">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div class="space-y-2">
                            <label class="text-xs font-black text-gray-400 uppercase tracking-widest">Select Student *</label>
                            <select name="student_id" required class="w-full px-5 py-3 bg-gray-50 border border-gray-100 rounded-2xl outline-none focus:border-accent focus:bg-white transition-all text-sm font-bold text-gray-500">
                                <option value="">Search Student...</option>
                                <?php foreach($students as $s): ?>
                                    <option value="<?php echo $s['id']; ?>"><?php echo $s['first_name'].' '.$s['last_name'].' ('.$s['admission_no'].')'; ?></option>
                                <?php endforeach; ?>
                            </select>
                        </div>
                        <div class="space-y-2">
                            <label class="text-xs font-black text-gray-400 uppercase tracking-widest">Fee Category *</label>
                            <select name="category_id" required class="w-full px-5 py-3 bg-gray-50 border border-gray-100 rounded-2xl outline-none focus:border-accent focus:bg-white transition-all text-sm font-bold text-gray-500">
                                <?php foreach($categories as $cat): ?>
                                    <option value="<?php echo $cat['id']; ?>"><?php echo $cat['category_name']; ?></option>
                                <?php endforeach; ?>
                            </select>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div class="space-y-2">
                            <label class="text-xs font-black text-gray-400 uppercase tracking-widest">Amount to Pay *</label>
                            <div class="relative">
                                <span class="absolute left-5 top-1/2 -translate-y-1/2 text-gray-400 font-bold"><?php echo CURRENCY; ?></span>
                                <input type="number" name="amount_paid" required class="w-full pl-10 pr-5 py-3 bg-gray-50 border border-gray-100 rounded-2xl outline-none focus:border-accent focus:bg-white transition-all text-sm font-bold" placeholder="0.00">
                            </div>
                        </div>
                        <div class="space-y-2">
                            <label class="text-xs font-black text-gray-400 uppercase tracking-widest">Payment Method *</label>
                            <select name="payment_method" required class="w-full px-5 py-3 bg-gray-50 border border-gray-100 rounded-2xl outline-none focus:border-accent focus:bg-white transition-all text-sm font-bold text-gray-500">
                                <option value="Cash">Cash</option>
                                <option value="Online">Online / UPI</option>
                                <option value="Cheque">Cheque</option>
                                <option value="Bank Transfer">Bank Transfer</option>
                            </select>
                        </div>
                    </div>

                    <div class="space-y-2">
                        <label class="text-xs font-black text-gray-400 uppercase tracking-widest">Remarks / Description</label>
                        <textarea name="remarks" rows="2" class="w-full px-5 py-3 bg-gray-50 border border-gray-100 rounded-2xl outline-none focus:border-accent focus:bg-white transition-all text-sm font-bold" placeholder="Optional notes..."></textarea>
                    </div>

                    <div class="pt-4">
                        <button type="submit" class="w-full py-4 bg-erp_green text-white rounded-[20px] font-black text-sm shadow-2xl shadow-erp_green/30 hover:scale-[1.02] transition-all flex items-center justify-center gap-3">
                            <i class="fas fa-check-circle"></i> Generate Receipt & Save
                        </button>
                    </div>
                </div>
            </form>
        </div>

        <!-- Info Sidebar -->
        <div class="space-y-8">
            <div class="bg-white p-8 rounded-[40px] border border-gray-100 shadow-sm">
                <h4 class="text-sm font-black text-primary uppercase tracking-widest mb-6">Student Due Info</h4>
                <div class="flex flex-col items-center justify-center py-10 text-center space-y-4">
                    <div class="w-20 h-20 bg-gray-50 rounded-full flex items-center justify-center text-gray-200 text-3xl">
                        <i class="fas fa-user-clock"></i>
                    </div>
                    <p class="text-gray-400 text-xs font-bold uppercase px-6">Select a student to view pending dues and scholarship eligibility.</p>
                </div>
            </div>

            <div class="bg-primary p-8 rounded-[40px] text-white shadow-2xl shadow-primary/30">
                <h4 class="text-sm font-black uppercase tracking-widest mb-4">Security Warning</h4>
                <p class="text-xs text-white/60 leading-relaxed">Ensure the correct academic year is selected before posting payments. Receipts once generated cannot be modified by staff.</p>
            </div>
        </div>
    </div>
</div>

<?php require_once '../../includes/footer.php'; ?>
