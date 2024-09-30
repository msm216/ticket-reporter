document.addEventListener('DOMContentLoaded', function () {
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
function openModal(id, mode, objectType) {
    // 获取模态框模块
    const moodalID = `${objectType}${capitalizeFirstLetter(mode)}Modal`;;
    console.log("Dynamic modal ID: ", moodalID);
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

    // 根据不同模式获取数据并填充表单
    fetch(`/load-form?mode=${mode}&objectType=${objectType}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(data => {
            // 把获取的内容插入到id为 modalForm 的区块中
            document.getElementById('modalForm').innerHTML = data;

            // 根据不同的 modalMode 动态设置 modalForm 的 action 路径
            var modalForm = modalModule.querySelector('.modal-form');
            modalForm.action = id ? `/${objectType}/${id}/${mode}` : `/${objectType}/${mode}`;
            console.log("Form action URL: ", modalForm.action);

            // 表单加载后显示模态框
            modalModule.style.display = "block";
            //modalModule.classList.add('is-active');
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    
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
        const deleteUrl = `/${objectType}/${id}/delete`;
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
function printInstance(id, objectType) {
    const printUrl = `/${objectType}/${id}/print`;
    window.open(printUrl, '_blank');
    console.log('Printing', objectType, id);
}

// 打印主题
function printTheme(objectType) {
    const printUrl = `/${objectType}/print/`;
    window.open(printUrl, '_blank');
    console.log('Printing', objectType);
}

// 重置筛选条件并重新加载页面
function resetFilters(resetUrl) {
    // 获取表单元素
    // 设置默认日期和其他参数
    const defaultStartDate = '2022-01-01';
    const defaultFilterBy = 'none';
    // 构建重置后的 URL
    const resetParams = `?start_date=${defaultStartDate}&filter-by=${defaultFilterBy}`;
    // 使用从模板中传递的 resetUrl 来重定向
    window.location.href = resetUrl + resetParams;
    console.log('Reset filter...');
}