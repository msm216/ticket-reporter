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

// 关闭模态框
function closeModal() {
    var modal = document.getElementById("modalModule");
    //modal.classList.remove('is-active');
    modal.style.display = "none"; // 隐藏模态框
}
// 点击模态框背景区域关闭
window.onclick = function(event) {
    var modal = document.getElementById("modalModule");
    if (event.target === modal) {
        closeModal();
    }
}

// 字符串首字母大写
function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}
// 开启模态框
function openModal(id, mode, objectType) {
    // 获取模态框模块
    const modalModule = document.getElementById('modalModule');
    
    // 处理标题
    var titleActionSection = document.getElementById('titleActionSection');
    var titleObjectSection = document.getElementById('titleObjectSection');
    var titleIdSection = document.getElementById('titleIdSection');
    titleActionSection.textContent = mode ? capitalizeFirstLetter(mode) : 'Action';
    titleObjectSection.textContent = objectType ? capitalizeFirstLetter(objectType) : 'Object';
    titleIdSection.textContent = id ? ` ${id}` : '';
    
    // 获取按钮元素
    var modalSubmit = document.getElementById('modalSubmit');
    var modalButtton = document.getElementById('modalButton');
    
    // 赋值隐藏元素
    document.getElementById('instId').value = id || '';
    document.getElementById('modalMode').value = mode;
    var modalMode = document.getElementById('modalMode').value;
    console.log("Modal mode: ", modalMode);

    // 动态设置 modalForm 的 action 路径
    var modalForm = modalModule.querySelector('.modal-form');
    modalForm.action = id ? `/${objectType}/${mode}/${id}` : `/${objectType}/${mode}`;
    console.log("Form action URL: ", modalForm.action);
    
    // 获取表单内容区域
    var titleInput = document.getElementById('title');
    var descriptionInput = document.getElementById('description');

    // 根据不同模式获取数据并填充表单
    if (mode === 'edit') {
        console.log("Fetch: ", `/${objectType}/${id}`);
        // 获取 issue 数据 (假设通过 AJAX 从服务器获取数据)
        fetch(`/${objectType}/${id}`)
            .then(response => response.json())
            .then(data => {
                titleInput.value = data.title;
                descriptionInput.value = data.description;
            })
            .catch(error => console.log(error));
    } else if (mode === 'update') {
        // 对于 Resolution 的更新，可能不需要获取现有数据，只需要输入新的描述
        titleInput.parentElement.style.display = 'none'; // 隐藏 title 字段
        descriptionInput.value = ''; // 清空描述字段，用于新建 Resolution
    }

    // 根据不同的 modalMode 动态赋予不同的函数给 Test 按钮
    if (mode === 'add') {
        modalButtton.onclick = addInstance;
    } else if (mode === 'edit') {
        modalButtton.onclick = editInstance;
    } else if (mode === 'update') {
        modalButtton.onclick = updateInstance;
    } else {
        modalButtton.onclick = null;
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
function deleteInstance(id, objectType) {
    confirmAction('Are you sure you want to delete this instance?', function() {
        fetch(objectType + '/delete/' + id, {
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

// 打印实例
function printInstance(id, objectType) {
    const printUrl = `/${objectType}/print/${id}`;
    window.open(printUrl, '_blank');
    console.log('Printing modal...');
}