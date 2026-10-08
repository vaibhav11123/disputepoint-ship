import { cva, type VariantProps } from "class-variance-authority"
import type { HTMLAttributes } from "react"
import { cn } from "../../lib/cn"

const badgeVariants = cva("dp-badge", {
  variants: {
    variant: {
      default: "dp-badge-default",
      warn: "dp-badge-warn",
      danger: "dp-badge-danger",
      ok: "dp-badge-ok",
      muted: "dp-badge-muted",
    },
  },
  defaultVariants: { variant: "default" },
})

export function Badge({
  className,
  variant,
  ...props
}: HTMLAttributes<HTMLSpanElement> & VariantProps<typeof badgeVariants>) {
  return <span className={cn(badgeVariants({ variant }), className)} {...props} />
}
