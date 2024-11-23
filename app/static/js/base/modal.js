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