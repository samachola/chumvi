//Page animations here

var $logo = $(".logoo");
$logo.velocity({
    translateY: "10px"
}, {
    loop: true
}).velocity("reverse");