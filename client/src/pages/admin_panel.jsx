import * as React from 'react';
import PropTypes from 'prop-types';
import Box from '@mui/material/Box';
import { createTheme } from '@mui/material/styles';
import DashboardIcon from '@mui/icons-material/Dashboard';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import { AppProvider } from '@toolpad/core/AppProvider';
import { DashboardLayout } from '@toolpad/core/DashboardLayout';
import { useDemoRouter } from '@toolpad/core/internal';
import { PageContainer } from '@toolpad/core/PageContainer';
import StudentTable from '../components/table/table';
import { useNavigate } from "react-router-dom";
import PersonIcon from '@mui/icons-material/Person';
import LaptopChromebookIcon from '@mui/icons-material/LaptopChromebook';

const demoTheme = createTheme({
  cssVariables: {
    colorSchemeSelector: 'data-toolpad-color-scheme',
  },
  colorSchemes: { light: true, dark: true },
  breakpoints: {
    values: {
      xs: 0,
      sm: 600,
      md: 600,
      lg: 2000,
      xl: 1536,
    },
  },
});

function DemoPageContent({ pathname, navigate }) {
  return (
    <Box
      sx={{
        py: 4,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        textAlign: 'center',
      }}
    >
      {pathname.startsWith('/students') ? (<StudentTable/>) : null}
    </Box>
  );
}

DemoPageContent.propTypes = {
  navigate: PropTypes.func.isRequired,
  pathname: PropTypes.string.isRequired,
};
const NAVIGATION = [
  {
    kind: 'header',
    title: 'Главная',
  },
  {
    segment: 'dashboard',
    title: 'Главная',
    icon: <DashboardIcon />,
  },
  {
    kind: 'divider',
  },
  {
    kind: 'header',
    title: 'Информация',
  },
  {
    segment: 'students',
    title: 'Студенты',
    icon: <PersonIcon/>
  },
  {
    segment: 'online_course',
    title: 'Онлайн курсы',
    icon: <LaptopChromebookIcon />,
  },
  {
    kind: 'divider',
  },
  {
    kind: 'header',
    title: 'Analytics',
  },
  {
    segment: 'reports',
    title: 'Reports',
    icon: <ShoppingCartIcon />,
    children: [
      {
        segment: 'sales',
        title: 'Sales',
        icon: <ShoppingCartIcon />,
      },
      {
        segment: 'traffic',
        title: 'Traffic',
        icon: <ShoppingCartIcon />,
      },
      {
        segment: 'traffic',
        title: 'Traffic',
        icon: <ShoppingCartIcon />,
        children: [
          {
            segment: 'sales',
            title: 'Sales',
            icon: <ShoppingCartIcon />,
          }
        ],
      },
    ],
  },
  {
    segment: 'integrations',
    title: 'Integrations',
    icon: <ShoppingCartIcon />,
  },
];

function Navigate(props) {

  const navigate = useNavigate();

  React.useEffect(() => {
    if (sessionStorage.getItem("token") == null){
      navigate("/sing_in_admin")
    }
  })

  const { window } = props;

  const router = useDemoRouter('/dashboard');

  // Remove this const when copying and pasting into your project.
  const demoWindow = window !== undefined ? window() : undefined;

  return (
    // preview-start
    <AppProvider
      navigation={NAVIGATION}
      router={router}
      theme={demoTheme}
      window={demoWindow}
    >
      <DashboardLayout>
        <PageContainer> 
          <DemoPageContent pathname={router.pathname} navigate={router.navigate} />
        </PageContainer>
      </DashboardLayout>
    </AppProvider>
    // preview-end
  );
}

Navigate.propTypes = {
  /**
   * Injected by the documentation to work in an iframe.
   * Remove this when copying and pasting into your project.
   */
  window: PropTypes.func,
};

export default Navigate;
