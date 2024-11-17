import style from './card.module.css'

export default function Card({title, discr, price, sizes}){

    const get_sizes = (sizes) => {
        let str = "["
        sizes.map((size) => (str = str + size + ", "))
        return str.slice(0, str.length - 2) + "]"
      }

    return (
        <li className={style.card}>
            <h3 className={style.title}>Название {title}</h3>
            <h4 className={style.discr}>Описание {discr}</h4>
            <h4 className={style.price}>Цена {price}</h4>
            <h4 className={style.price}>Размеры {get_sizes(sizes)}</h4>
            <button>Добавить</button>
        </li>
    )
}