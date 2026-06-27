import { useState } from "react";
import { ChevronDown } from "lucide-react";
import ProfileDropdown from "./ProfileDropdown";
import { User2 } from "lucide-react";
import UserDummy from "../../../assets/user_dummy.png";
import { useSelector } from "react-redux";
const ProfileMenu = () => {
  const [open, setOpen] = useState(false);
  const { user } = useSelector((state) => state.auth);
  return (
    <div className="relative">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-3 px-2 py-1 rounded-xl hover:bg-slate-100"
      >
        <img
          src={user?.profile?.image_url || UserDummy}
          alt=""
          className="w-8 h-8 rounded-full"
        />

        <div className="hidden text-left md:block">
          <h4 className="text-sm font-semibold">{user?.profile?.full_name}</h4>

          <p className="text-xs text-slate-500">{user?.role}</p>
        </div>

        <ChevronDown size={18} />
      </button>

      {open && <ProfileDropdown />}
    </div>
  );
};

export default ProfileMenu;
