import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"
import type { ButtonHTMLAttributes } from "react"
import { cn } from "../../lib/cn"

const buttonVariants = cva("dp-btn", {
  variants: {
    variant: {
      default: "dp-btn-default",
      outline: "dp-btn-outline",
      ghost: "dp-btn-ghost",
      danger: "dp-btn-danger",
    },
    size: {
      default: "dp-btn-md",
      sm: "dp-btn-sm",
      lg: "dp-btn-lg",
    },
  },
  defaultVariants: { variant: "default", size: "default" },
})

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement>, VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

export function Button({ className, variant, size, asChild = false, ...props }: ButtonProps) {
  const Comp = asChild ? Slot : "button"
  return <Comp className={cn(buttonVariants({ variant, size }), className)} {...props} />
}
