import Logo from "./NavBar/Logo";
import SearchBar from "./NavBar/SearchBar";
import CreateCompanyButton from "./NavBar/CreateCompanyButton";
import NotificationButton from "./NavBar/NotificationButton";
import ProfileMenu from "./NavBar/ProfileMenu";

const Navbar = () => {
  return (
    <header className="sticky top-0 z-50 bg-white border-b shadow-sm">
      <div className="flex items-center justify-between h-16 px-6 mx-auto max-w-7xl">
        <Logo />

        <SearchBar />

        <div className="flex items-center gap-3">
          <CreateCompanyButton />
          <NotificationButton />
          <ProfileMenu />
        </div>
      </div>
    </header>
  );
};

export default Navbar;
