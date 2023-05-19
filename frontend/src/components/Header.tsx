import {Link} from 'react-router-dom';
import Logo from '../images/logo/logo-icon.svg';
import DarkModeSwitcher from './DarkModeSwitcher';
import DropdownMessage from './DropdownMessage';
import DropdownNotification from './DropdownNotification';
import DropdownUser from './DropdownUser';

const Header = (props: {
  sidebarOpen: string | boolean | undefined;
  setSidebarOpen: (arg0: boolean) => void;
}) => {
  return (
    <header className="flex flex-col w-full bg-white drop-shadow-1 dark:bg-boxdark dark:drop-shadow-none">
      {/*<div className="flex flex-grow items-center justify-between py-4 px-4 shadow-2 md:px-6 2xl:px-11">*/}
      <div className="font-serif font-bold text-5xl text-center w-full py-4 px-4 shadow-2 md:px-6 2xl:px-11">
        Homelessness in Australia
      </div>
      {/*</div>*/}
    </header>
  );
};

export default Header;
