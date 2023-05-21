import DarkModeSwitcher from './DarkModeSwitcher';


const Header = () => {
  return (

    <header className="sticky top-0 z-999 flex w-full bg-white drop-shadow-1 dark:bg-boxdark dark:drop-shadow-none">
      <div className="flex flex-grow items-center justify-between py-4 px-4 shadow-2 md:px-6 2xl:px-11">
        <div className="hidden sm:block">
          <form action="https://formbold.com/s/unique_form_id" method="POST">
            <div className="relative">
              <div className="w-full bg-transparent pr-4 pl-9 text-3xl">
                Homelessness in Australia
              </div>
            </div>
          </form>
        </div>

        <div className="flex items-center gap-3 2xsm:gap-7">
          <ul className="flex items-center gap-2 2xsm:gap-4">
            <DarkModeSwitcher/>
          </ul>
        </div>
      </div>
    </header>
  );
};

export default Header;
