import style from './list_shoes.module.css'
import Card from '../card_shoe/card'

export default function ListShoes({shoes = []}) {
    return (
        <div class="container">
            <ul className={style.list}>
                {
                    shoes.map(shoe => {
                        return <Card title={shoe.title} discr={shoe.discr} price={shoe.price} sizes={shoe.sizes}/>
                    })
                }
            </ul>
        </div>
    )
}