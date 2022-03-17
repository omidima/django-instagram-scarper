var header = document.getElementsByTagName('header')[0];
var isFixed = false;
document.addEventListener('scroll', handleHeader)

function handleHeader(e) {
    if (window.scrollY > 80 && !isFixed) {
        header.style.position = 'fixed';
        isFixed = true
    }else if (window.scrollY <= 80 && isFixed) {
        header.style.position = '';
        isFixed = false
    }
}