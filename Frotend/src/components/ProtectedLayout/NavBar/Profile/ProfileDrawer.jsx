import { X } from "lucide-react";
import ProfileCard from "./ProfileCard";
import ProfileStats from "./ProfileStats";

const ProfileDrawer = ({ open, onClose }) => {
  return (
    <>
      {/* Overlay */}

      <div
        onClick={onClose}
        className={`fixed inset-0 z-40 bg-black/40 transition-all duration-300 ${
          open ? "visible opacity-100" : "invisible opacity-0"
        }`}
      />

      {/* Drawer */}

      <div
        className={`fixed right-0 top-0 z-50 h-screen w-[420px] bg-white shadow-2xl transition-all duration-300 ${
          open ? "translate-x-0" : "translate-x-full"
        }`}
      >
        {/* Header */}

        <div className="flex items-center justify-between p-6 border-b">
          <h2 className="text-2xl font-bold">My Profile</h2>

          <button
            onClick={onClose}
            className="p-2 rounded-lg hover:bg-slate-100"
          >
            <X />
          </button>
        </div>

        {/* Body */}

        <div className="p-6 space-y-8">
          <ProfileCard />

          <ProfileStats />

          {/* Information */}

          <div className="space-y-4">
            <div>
              <p className="text-sm text-slate-500">Email</p>

              <h4 className="font-medium">shekhar@gmail.com</h4>
            </div>

            <div>
              <p className="text-sm text-slate-500">Phone</p>

              <h4 className="font-medium">+977 98XXXXXXXX</h4>
            </div>

            <div>
              <p className="text-sm text-slate-500">Country</p>

              <h4 className="font-medium">Nepal</h4>
            </div>
          </div>

          {/* Buttons */}

          <div className="space-y-3">
            <button className="w-full py-3 font-semibold text-white bg-blue-600 rounded-xl hover:bg-blue-700">
              Edit Profile
            </button>

            <button className="w-full py-3 font-semibold border rounded-xl hover:bg-slate-100">
              Change Password
            </button>

            <button className="w-full py-3 font-semibold text-white bg-red-600 rounded-xl hover:bg-red-700">
              Logout
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

export default ProfileDrawer;
