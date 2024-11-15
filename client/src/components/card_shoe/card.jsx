import style from './card.module.css'

export default function Card({title, discr, price}){

    return (
        <li className={style.card}>
            <h3 className={style.title}>{title}</h3>
            <h4 className={style.discr}>{discr}</h4>
            <h4 className={style.price}>{price}</h4>
            <button>Добавить</button>
        </li>
    )
}