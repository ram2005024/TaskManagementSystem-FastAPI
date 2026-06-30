import CompanySearchItem from "./CompanySearchItem";

const SearchDropdown = ({ companies }) => {
  return (
    <div className="absolute w-full mt-2 bg-white border shadow-xl rounded-xl">
      {companies.length ? (
        companies.map((company) => (
          <CompanySearchItem key={company.id} company={company} />
        ))
      ) : (
        <div className="p-6 text-sm text-center text-slate-500">
          No Company Found
        </div>
      )}
    </div>
  );
};

export default SearchDropdown;
