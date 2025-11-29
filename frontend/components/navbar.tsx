"use client"

import Link from "next/link"
import Image from "next/image"
import { usePathname } from 'next/navigation'
import { Package2, Upload, LayoutDashboard, Settings } from 'lucide-react'
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"

export function Navbar() {
  const pathname = usePathname()

  return (
    <nav className="border-b border-border bg-card/50 backdrop-blur-xl sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          <Link href="/dashboard" className="flex items-center gap-2 font-semibold text-lg">
            <div className="relative h-14 w-22 overflow-hidden rounded-lg">
              <Image
                src="/logos/logo1.png"
                alt="SmartStock AI Logo"
                fill
                className="object-cover"
              />
            </div>
            <span className="text-balance">SmartStock AI</span>
          </Link>

          <div className="flex items-center gap-2">
            <Button
              variant={pathname === "/upload" ? "default" : "ghost"}
              size="sm"
              asChild
            >
              <Link href="/upload" className="flex items-center gap-2">
                <Upload className="h-4 w-4" />
                <span className="hidden sm:inline">Upload Item</span>
              </Link>
            </Button>

            <Button
              variant={pathname === "/dashboard" ? "default" : "ghost"}
              size="sm"
              asChild
            >
              <Link href="/dashboard" className="flex items-center gap-2">
                <LayoutDashboard className="h-4 w-4" />
                <span className="hidden sm:inline">Dashboard</span>
              </Link>
            </Button>

            <Button
              variant={pathname === "/settings/product-types" ? "default" : "ghost"}
              size="sm"
              asChild
            >
              <Link href="/settings/product-types" className="flex items-center gap-2">
                <Settings className="h-4 w-4" />
                <span className="hidden sm:inline">Manage Types</span>
              </Link>
            </Button>
          </div>
        </div>
      </div>
    </nav>
  )
}
