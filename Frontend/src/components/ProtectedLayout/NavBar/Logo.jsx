const Logo = () => {
  return (
    <div className="flex items-center gap-3 cursor-pointer">
      <div className="flex items-center justify-center text-xl font-bold text-white bg-blue-600 h-11 w-11 rounded-xl">
        T
      </div>

      <div>
        <h2 className="text-lg font-bold text-slate-800">TaskFlow</h2>

        <p className="text-xs text-slate-500">Workspace Manager</p>
      </div>
    </div>
  );
};

export default Logo;
