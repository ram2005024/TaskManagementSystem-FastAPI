import { User, Settings, LogOut } from "lucide-react";
import { useState } from "react";
import ProfileDrawer from "./Profile/ProfileDrawer";

const ProfileDropdown = () => {
  const [myProfileOpen, setMyProfileOpen] = useState(false);
  const [setsettingOpen, setSetsettingOpen] = useState(false);
  return (
    <div className="absolute right-0 w-56 mt-2 bg-white border shadow-xl rounded-xl">
      <button
        onClick={() => setMyProfileOpen(true)}
        className="flex items-center w-full gap-3 px-4 py-3 hover:bg-slate-50"
      >
        <User size={18} />
        My Profile
      </button>

      <button className="flex items-center w-full gap-3 px-4 py-3 hover:bg-slate-50">
        <Settings size={18} />
        Settings
      </button>

      <hr />

      <button className="flex items-center w-full gap-3 px-4 py-3 text-red-600 hover:bg-red-50">
        <LogOut size={18} />
        Logout
      </button>
      <ProfileDrawer
        onClose={() => setMyProfileOpen(false)}
        open={myProfileOpen}
      />
    </div>
  );
};

export default ProfileDropdown;
