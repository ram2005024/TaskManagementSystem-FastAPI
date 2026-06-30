const ProfileCard = () => {
  return (
    <div className="flex flex-col items-center">
      <img
        src="https://i.pravatar.cc/200?img=32"
        className="border-4 border-blue-500 rounded-full h-28 w-28"
      />

      <h2 className="mt-4 text-2xl font-bold">Shekhar Sharma</h2>

      <p className="text-slate-500">Manager</p>
    </div>
  );
};

export default ProfileCard;
