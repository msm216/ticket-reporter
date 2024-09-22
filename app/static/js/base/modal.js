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

// 这里是 addInstance 的实现逻辑
function addInstance() {
    console.log('Adding instance...');
}

// 这里是 editInstance 的实现逻辑
function editInstance() {
    console.log('Editting modal...');
}

// 这里是 updateInstance 的实现逻辑
function updateInstance() {
    console.log('Updating instance...');
}

