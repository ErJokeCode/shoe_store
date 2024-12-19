import style from './footer.module.css'

export default function Footer() {
    return (
        <footer className={style.footer}>
            <div class="container">
                <div className={style.footer_info}>
                    <div className={style.footer__contacts}>
                        <h2>
                            Наши контакты
                        </h2>
    
                        <p>
                            телефон
                        </p>
    
                        <p>
                            почта
                        </p>
    
                        <p>
                            График работы
                        </p>
                    </div>
    
                    <div className={style.footer__secial}>
                        <p>*ссылки на соцсети*</p>
                    </div>
                </div>
            </div>
        </footer>
    )
}