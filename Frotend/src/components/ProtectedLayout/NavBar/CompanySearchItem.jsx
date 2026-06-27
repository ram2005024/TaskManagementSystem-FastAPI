import { Building2 } from "lucide-react";

const CompanySearchItem = ({ company }) => {
  return (
    <button className="flex items-center justify-between w-full px-4 py-3 transition hover:bg-slate-50">
      <div className="flex items-center gap-3">
        <Building2 size={18} className="text-blue-600" />

        <div className="text-left">
          <h3 className="font-medium">{company.name}</h3>

          <p className="text-xs text-slate-500">{company.members} Members</p>
        </div>
      </div>

      {company.joined ? (
        <span className="px-3 py-1 text-xs font-semibold text-green-700 bg-green-100 rounded">
          Joined
        </span>
      ) : (
        <button className="px-3 py-1 text-xs font-semibold text-white bg-blue-600 rounded hover:bg-blue-700">
          Join
        </button>
      )}
    </button>
  );
};

export default CompanySearchItem;
