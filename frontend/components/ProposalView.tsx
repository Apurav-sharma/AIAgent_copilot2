export default function ProposalView({ proposal }: any) {
  return (
    <div style={{ width: "40%", padding: 16 }}>
      <h3>Proposal Document</h3>

      {proposal ? (
        <pre style={{ whiteSpace: "pre-wrap" }}>{proposal}</pre>
      ) : (
        <p>No proposal yet.</p>
      )}
    </div>
  );
}
