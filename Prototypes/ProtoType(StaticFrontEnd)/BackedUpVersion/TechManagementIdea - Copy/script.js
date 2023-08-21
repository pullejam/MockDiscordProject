const side_Menu = document.getElementById(`side_Menu`);
const btn_Menu = document.getElementById(`menu_Button`);

const showMenu = () =>{
    side_Menu.style.display ="flex";
    btn_Menu.style.display = "none";
}
btn_Menu.addEventListener("click", showMenu)

const closeMenu = () =>{
    side_Menu.style.display = "none";
    btn_Menu.style.display = "inline"
}