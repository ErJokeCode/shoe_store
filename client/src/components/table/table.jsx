import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import axios from 'axios'


export default function BasicTable({is_sales = false}) {
  const [rows, setRows] = React.useState([])
  React.useEffect(() => {
    async function get_rows() {
      if (is_sales === false){
        const {data} = await axios.get(`http://${process.env.REACT_APP_SERVER_URL}/shoe`)
        setRows(data)
      }
      else{
        const {data} = await axios.get(`http://${process.env.REACT_APP_SERVER_URL}/shoe/sales`)
        setRows(data)
      }
    }
    get_rows()
  }, [])

  const get_sales = (sizes) => {
    let str = "["
    sizes.map((size) => (str = str + size + ", "))
    return str.slice(0, str.length - 2) + "]"
  }

  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>Номер</TableCell>
            <TableCell align="right">Название</TableCell>
            <TableCell align="right">Описание</TableCell>
            <TableCell align="right">Размеры</TableCell>
            <TableCell align="right">Цена</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <TableRow
              key={row.number}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell component="th" scope="row">
                {row.number}
              </TableCell>
              <TableCell align="right">{row.title}</TableCell>
              <TableCell align="right">{row.discr}</TableCell>
              <TableCell align="right">{get_sales(row.sizes)}</TableCell>
              <TableCell align="right">{row.price}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
