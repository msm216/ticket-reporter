document.addEventListener('DOMContentLoaded', function () {
    // 获取查询参数
    const queryParams = new URLSearchParams(window.location.search);
    // 打印所有查询参数
    queryParams.forEach((value, key) => {
        console.log(`${key}: ${value}`);
    });
    // 获取所有卡片对象
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

// 字符串首字母大写
function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}
// 开启模态框
function openModal(id, mode, objectClass) {
    // 获取模态框模块
    const moodalID = `${objectClass}${capitalizeFirstLetter(mode)}Modal`;
    console.log("Dynamic modal ID: ", moodalID);
    const modalModule = document.getElementById('modalModule');
    
    // 处理标题
    var titleActionSection = document.getElementById('titleActionSection');
    var titleObjectSection = document.getElementById('titleObjectSection');
    var titleIdSection = document.getElementById('titleIdSection');
    titleActionSection.textContent = mode ? capitalizeFirstLetter(mode) : 'Action';
    titleObjectSection.textContent = objectClass ? capitalizeFirstLetter(objectClass) : 'Object';
    titleIdSection.textContent = id ? ` ${id}` : '';
    
    // 获取按钮元素
    var modalSubmit = document.getElementById('modalSubmit');
    
    // 赋值隐藏元素
    document.getElementById('instId').value = id || '';
    document.getElementById('modalMode').value = mode;
    var modalMode = document.getElementById('modalMode').value;
    console.log("Modal mode: ", modalMode);

    // 传递参数到路由函数 load_form() 并获取返回的表单 HTML 内容
    fetch(`/load-form?modal-mode=${encodeURIComponent(mode)}&object-class=${encodeURIComponent(objectClass)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(data => {
            // 把获取的 HTML 内容插入到id为 modalForm 的区块中
            document.getElementById('modalContent').innerHTML = data;
            
            // 根据不同的 modalMode 动态设置 modalForm 的 action 路径
            var modalForm = modalModule.querySelector('.modal-form');
            modalForm.action = id ? `/${objectClass}/${id}/${mode}` : `/${objectClass}/${mode}`;
            console.log("Form action URL: ", modalForm.action);

            // 表单加载后显示模态框
            modalModule.style.display = "block";
            //modalModule.classList.add('is-active');
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    
    // 根据不同的 modalMode 动态赋予不同的函数给 Test 按钮
    var modalTestBtn = document.getElementById('modalTestBtn');
    if (mode === 'add') {
        modalTestBtn.onclick = addInstance;
    } else if (mode === 'edit') {
        modalTestBtn.onclick = editInstance;
    } else if (mode === 'update') {
        modalTestBtn.onclick = updateInstance;
    } else {
        modalTestBtn.onclick = null;
    }
}

// 确认弹窗
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// 删除实例
function deleteInstance(id, objectClass) {
    confirmAction('Are you sure you want to delete this instance?', function() {
        const deleteUrl = `/${objectClass}/${id}/delete`;
        fetch(deleteUrl, {
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
function printInstance(id, objectClass) {
    const printUrl = `/${objectClass}/${id}/print`;
    window.open(printUrl, '_blank');
    console.log('Printing', objectClass, id);
}

// 打印主题
function printTheme(objectClass) {
    const printUrl = `/${objectClass}/print/`;
    window.open(printUrl, '_blank');
    console.log('Printing', objectClass);
}