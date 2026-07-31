function DashboardCard({ title, value, icon, color }) {
  return (
    <div className="bg-white rounded-2xl shadow-md p-6 hover:shadow-xl transition duration-300">
      <div className="flex justify-between items-center">
        <div>
          <p className="text-gray-500 text-sm">{title}</p>
          <h2 className="text-3xl font-bold mt-2">{value}</h2>
        </div>

        <div className={`text-4xl ${color}`}>
          {icon}
        </div>
      </div>
    </div>
  );
}

export default DashboardCard;