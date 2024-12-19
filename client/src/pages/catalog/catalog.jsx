import React, { useEffect } from 'react';
import { Box, Button, Container, Typography } from '@mui/material';
import Grid from '@mui/material/Grid';
import Card from '../../components/card_shoe/card'
import { useNavigate } from "react-router-dom";
import style from "../catalog/catalog.module.css"
import { useState } from 'react';
import axios from "axios"

import Header from '../../components/header/header'
import Footer from '../../components/footer/footer'
import ListShoes from '../../components/list_shoes/list_shoes'


export default function Catalog() {
    const [shoes, setShoes] = useState([])
    const [is_sales, setIsSails] = useState(false)

    useEffect(() => {
        async function get_rows() {
            if (is_sales === false){
              const {data} = await axios.get(`http://${process.env.REACT_APP_SERVER_URL}/shoe`)
              setShoes(data)
            }
            else{
              const {data} = await axios.get(`http://${process.env.REACT_APP_SERVER_URL}/shoe/sales`)
              setShoes(data)
            }
          }
          get_rows()
    }, [])

    const navigate = useNavigate();

    console.log(shoes)
    return (
    <div>
      <Header></Header>
      <ListShoes shoes={shoes}></ListShoes>
      <Footer></Footer>
    </div>
  );
}