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


function openModal(id, mode, objectType) {
    // 获取模态框元素
    const modalModule = document.getElementById('modalModule');
    // modal.querySelector('.modal-title') 获取对象 modal 内第一个 modal-title 类

    var titleActionSection = document.getElementById('titleActionSection');
    var titleObjectSection = document.getElementById('titleObjectSection');
    var titleIdSection = document.getElementById('titleIdSection');
    var modalSubmit = document.getElementById('modalSubmit');
    
    // 赋值隐藏元素
    document.getElementById('instId').value = id;
    document.getElementById('modalMode').value = mode;

    // Title 第一部分：根据 mode 来设置操作名称 ("Add", "Edit", "Update")
    if (mode === 'add') {
        titleActionSection.textContent = 'Add';
    } else if (mode === 'edit') {
        titleActionSection.textContent = 'Edit';
    } else if (mode === 'update') {
        titleActionSection.textContent = 'Update';
    } else {
        titleActionSection.textContent = 'Action';
    }
    // Title 第二部分：根据 objectType 来设置对象类型 ("Issue", "Ticket")
    if (objectType === 'issue') {
        titleObjectSection.textContent = 'Issue';
    } else if (objectType === 'ticket') {
        titleObjectSection.textContent = 'Ticket';
    } else {
        titleObjectSection.textContent = 'Object';
    }
    // Title 第三部分：只要输入的 id 非 null 就显示 id，否则不显示
    titleIdSection.textContent = id ? ` ${id}` : '';

    // 根据不同的 modalMode 动态赋予不同的函数给 Submit 按钮
    if (mode === 'add') {
        modalSubmit.onclick = addInstance;
    } else if (mode === 'edit') {
        modalSubmit.onclick = editInstance;
    } else if (mode === 'update') {
        modalSubmit.onclick = updateInstance;
    } else {
        modalSubmit.onclick = null;
    }

    //modalModule.classList.add('is-active'); // 显示模态框
    modalModule.style.display = "block"; // 显示模态框
}

// 确认弹窗
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}
// 删除实例
function deleteInstance(id) {
    confirmAction('Are you sure you want to delete this instance?', function() {
        fetch('/delete/' + id, {
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