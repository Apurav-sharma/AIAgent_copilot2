export default function CompanySelector({ options, onSelect }: any) {
  return (
    <div style={{ width: "30%", padding: 16, borderLeft: "1px solid #333" }}>
      <h3>Select Company</h3>

      {options.map((c: any) => (
        <button
          key={c.id}
          onClick={() => onSelect(c)}
          style={{ display: "block", marginBottom: 8 }}
        >
          {c.name}
        </button>
      ))}
    </div>
  );
}
