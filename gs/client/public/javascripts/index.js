/**
 * Created by 99100 on 2018/2/6.
 */
window.addEventListener('load', function () {
    // 在窗体载入完毕后再绑定
    var CM = new CommentManager($('#my-comment-stage'));
    CM.init();
    // 先启用弹幕播放（之后可以停止）
    CM.start();
    // 开放 CM 对象到全局这样就可以在 console 终端里操控
    window.CM = CM;
});