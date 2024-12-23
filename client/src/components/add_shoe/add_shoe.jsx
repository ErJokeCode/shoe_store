import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import { useState } from 'react';
import axios from "axios"


export default function Add_shoes() {
    const [num, setNum] = useState("")
    const [title, setTitle] = useState("")
    const [discr, setDiscr] = useState("")
    const [sales, setSales] = useState("Не в рапродаже")
    const [price, setPrice] = useState("")
    const [sizes, setSizes] = useState("")

    const add = async() => {
        console.log(num, title, discr, sales, price, sizes)
        let is_sales = true
        if (sales === "Не в рапродаже"){
            is_sales = false
        }

        var split_sizes = sizes.split()
        var float_sizes = []
        split_sizes.forEach(size => {
          float_sizes.push(parseFloat(size))
        });

        var data = {
          "title" : title, 
          "discr" : discr, 
          "sales" : is_sales, 
          "price" : price, 
          "sizes" : float_sizes
        }

        const config = {
            headers: {
              Authorization: `Bearer ${sessionStorage.getItem("token")}`,
            },
          };
        

        await axios.post(`http://${process.env.REACT_APP_SERVER_URL}/shoe`, data, { ...config })


        setNum("")
        setTitle("")
        setDiscr("")
        setSales("Не в рапродаже")
        setPrice("")
        setSizes("")
    }

    const currencies = [
        {
            value: false,
            label: 'Не в распродаже',
          },
        {
          value: true,
          label: 'В распродаже',
        }
      ];

    return (
        <Box
      component="form"
      sx={{ '& .MuiTextField-root': { m: 1, width: '100ch' } }}
      noValidate
      autoComplete="off"
    >
        <Box>
            <TextField
          required
          id="outlined-required"
          label="Номер артикула"
          defaultValue=""
          onChange={event => {setNum(event.target.value)}}
          value={num}
        />
        </Box>

        <Box>
            <TextField
          required
          id="outlined-required"
          label="Название"
          defaultValue=""
          onChange={event => {setTitle(event.target.value)}}
          value={title}
        />
        </Box>

        <Box>
            <TextField
          id="outlined-multiline-static"
          label="Описание"
          multiline
          rows={4}
          defaultValue=""
          onChange={event => {setDiscr(event.target.value)}}
          value={discr}
        />
        </Box>
        
        <Box>
            <TextField
          id="outlined-select-currency-native"
          select
          label="Sales"
          slotProps={{
            select: {
              native: true,
            },
          }}
          onChange={event => {setSales(event.target.value)}}
          value={sales}
        >
          {currencies.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </TextField>
        </Box>

        <Box>
            <TextField
            required
            id="outlined-number"
            label="Цена"
            type="number"
            slotProps={{
                inputLabel: {
                shrink: true,
                },
            }}
            onChange={event => {setPrice(event.target.value)}}
            value={price}
            />
        </Box>

        <Box>
            <TextField
          id="outlined-multiline-static"
          label="Размеры"
          multiline
          rows={2}
          defaultValue=""
          helperText="Впишите размеры через пробел"
          onChange={event => {setSizes(event.target.value)}}
          value={sizes}
        />
        </Box>

        <Button variant="contained" size="large" onClick={e => {add()}}>Добавить</Button>
    </Box>
    )
}