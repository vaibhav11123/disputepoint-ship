export function EvalDrawer({ onClose }: { onClose: () => void }) {
  return (
    <div className="palette" role="dialog" aria-label="Baseline tournament">
      <form
        onSubmit={(event) => {
          event.preventDefault()
          onClose()
        }}
      >
        <p>Report path: tests/eval/baseline_tournament.md</p>
        <p>Gold metrics: TBD. Spearman, Kendall, and top-k stay blank until a gold order exists.</p>
        <p>ML row omitted.</p>
        <button type="submit">Close</button>
      </form>
    </div>
  )
}
