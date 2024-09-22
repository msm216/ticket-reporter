function openIssueModal(mode, title, submitText) {
    const modal = document.getElementById('modalModule');
    const modalTitle = modal.querySelector('.modal-title');
    const submitButton = modal.querySelector('.modal-control .btn-primary');

    modalTitle.textContent = title || 'Default Title';
    submitButton.textContent = submitText || 'Submit';

    // 显示模态框
    modal.style.display = 'block';
}



// Add User: openModal(null, null, 'add')
// Edit: openModal(1, 'Alice', 'edit')
function openUserModal(id, name, registered_date, group_id, mode) {
    // 设置隐藏字段
    // 如果 || 左边对象为真值则以左边对象赋值，假值则用右边对象
    // 假值包括：false，0，-0，0n，null，""，undefined，NaN
    document.getElementById('userId').value = id || '';
    document.getElementById('userName').value = name || '';
    document.getElementById('userGroupID').value = group_id || '';
    console.log('Current group ID: ', mode)
    document.getElementById('userRegisteredOn').value = registered_date || '';
    // 影响模态框submit功能
    document.getElementById('userModalMode').value = mode;
    // 动态调整模态框标题和按钮文本
    // 三元运算符 variable = condition ? A : B
    // 如果 condition 满足（mode === 'add'）则赋值为 A 否则 B
    document.getElementById('userModalTitle').innerText = mode === 'add' ? 'Add User' : 'Edit User';
    document.getElementById('userModalSubmitButton').innerText = mode === 'add' ? 'Add User' : 'Save Changes';
    // 显示模态框
    document.getElementById('userModal').classList.add('is-active');
}