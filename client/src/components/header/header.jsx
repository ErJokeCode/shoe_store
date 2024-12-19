import style from './header.module.css'

export default function Header() {
    return (
        <header className={style.header}>
            <div class="container">
                <nav className={style.header_nav}>
                    <p className={style.logo}>Логотип</p>
    
                    <ul className={style.menu}>
                        <li className={style.item_menu}><a href="">Каталог</a></li>
                        <li className={style.item_menu}><a href="">Sale</a></li>
                        <li className={style.item_menu}><a href="">FAQ</a></li>
                        <li className={style.item_menu}><a href="">О компании</a></li>
                    </ul>
                </nav>
            </div>
        </header>
    )
}