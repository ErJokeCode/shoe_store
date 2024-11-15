import React from 'react';
import { Box, Button, Container, Typography } from '@mui/material';
import Grid from '@mui/material/Grid';
import Card from '../../components/card_shoe/card'
import { useNavigate } from "react-router-dom";
import style from "../catalog/catalog.module.css"



export default function Catalog() {

    const navigate = useNavigate();

    return (
    <div class="container">
        <h2 className={style.title}>Каталог</h2>
        <ul className={style.list_catalog}>
            <Card title={"djfhsj"} discr={"dfjhshdfj shdkfjhsdj kfhsjdkfskdf"} price={"12334"}/>
            <Card title={"djfhsj"} discr={"dfjhshdfj shdkfjhsdj kfhsjdkfskdf"} price={"12334"}/>
            <Card title={"djfhsj"} discr={"dfjhshdfj shdkfjhsdj kfhsjdkfskdf"} price={"12334"}/>
            <Card title={"djfhsj"} discr={"dfjhshdfj shdkfjhsdj kfhsjdkfskdf"} price={"12334"}/>
            <Card title={"djfhsj"} discr={"dfjhshdfj shdkfjhsdj kfhsjdkfskdf"} price={"12334"}/>
            <Card title={"djfhsj"} discr={"dfjhshdfj shdkfjhsdj kfhsjdkfskdf"} price={"12334"}/>
            <Card title={"djfhsj"} discr={"dfjhshdfj shdkfjhsdj kfhsjdkfskdf"} price={"12334"}/>
            <Card title={"djfhsj"} discr={"dfjhshdfj shdkfjhsdj kfhsjdkfskdf"} price={"12334"}/>
            <Card title={"djfhsj"} discr={"dfjhshdfj shdkfjhsdj kfhsjdkfskdf"} price={"12334"}/>
        </ul>
    </div>
  );
}