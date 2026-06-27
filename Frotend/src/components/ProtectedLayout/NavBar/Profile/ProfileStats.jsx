const ProfileStats = () => {
  return (
    <div className="grid grid-cols-3 gap-4">
      <div className="p-4 text-center rounded-xl bg-slate-100">
        <h2 className="text-2xl font-bold">4</h2>

        <p className="text-sm text-slate-500">Companies</p>
      </div>

      <div className="p-4 text-center rounded-xl bg-slate-100">
        <h2 className="text-2xl font-bold">182</h2>

        <p className="text-sm text-slate-500">Tasks</p>
      </div>

      <div className="p-4 text-center rounded-xl bg-slate-100">
        <h2 className="text-2xl font-bold">92%</h2>

        <p className="text-sm text-slate-500">Success</p>
      </div>
    </div>
  );
};

export default ProfileStats;
