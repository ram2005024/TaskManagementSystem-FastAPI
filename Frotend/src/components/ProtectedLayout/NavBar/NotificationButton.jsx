import { Bell } from "lucide-react";

const NotificationButton = () => {
  return (
    <button className="relative p-2 transition rounded-xl hover:bg-slate-100">
      <Bell size={21} />

      <span className="absolute w-2 h-2 bg-red-500 rounded-full right-2 top-2"></span>
    </button>
  );
};

export default NotificationButton;
