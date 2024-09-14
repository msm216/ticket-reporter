document.addEventListener('DOMContentLoaded', function () {
    //
    const toggleButtons = document.querySelectorAll('.toggle-icon');
    // 展开收缩卡片
    toggleButtons.forEach(button => {
        const collapseElementId = button.getAttribute('data-target');
        const collapseElement = document.querySelector(collapseElementId);
        // Collapse show event
        collapseElement.addEventListener('show.bs.collapse', () => {
            button.querySelector('i').classList.remove('fa-chevron-down');
            button.querySelector('i').classList.add('fa-chevron-up');
        });
        // Collapse hide event
        collapseElement.addEventListener('hide.bs.collapse', () => {
            button.querySelector('i').classList.remove('fa-chevron-up');
            button.querySelector('i').classList.add('fa-chevron-down');
        });
    });
});


function openIssueModal(id, mode) {
    // 设置隐藏字段
    // 如果 || 左边对象为真值则以左边对象赋值，假值则用右边对象
    // 假值包括：false，0，-0，0n，null，""，undefined，NaN
    document.getElementById('issueId').value = id;
    document.getElementById('issueModalMode').value = mode;
    console.log('Current group ID: ', id)
    console.log('Open modal in mode: ', mode)
    // 动态调整模态框标题和按钮文本
    // 三元运算符 variable = condition ? A : B
    // 如果 condition 满足（mode === 'add'）则赋值为 A 否则 B
    document.getElementById('issueModalTitle').innerText = mode === 'add' ? 'Add Issue' : 'Edit Issue';
    document.getElementById('issueModalSubmitButton').innerText = mode === 'add' ? 'Add Issue' : 'Save Changes';
    // 显示模态框
    const modal = document.getElementById('issueModal');
    console.log('Modal element:', modal);  // 检查modal元素
    //modal.classList.add('is-active'); // 显示模态框
    modal.style.display = "block"; // 显示模态框
}

function closeModal() {
    var modal = document.getElementById("issueModal");
    //modal.classList.remove('is-active');
    modal.style.display = "none"; // 隐藏模态框
}

window.onclick = function(event) {
    var modal = document.getElementById("issueModal");
    if (event.target === modal) {
        closeModal();
    }
}

// 确认弹窗
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}
// 删除实例
function deleteIssue(id) {
    confirmAction('Are you sure you want to delete this issue?', function() {
        fetch('/delete_user/' + id, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            }
        });
    });
}