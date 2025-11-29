import Link from "next/link"
import { Home, Package } from 'lucide-react'
import { Button } from "@/components/ui/button"

export default function NotFound() {
  return (
    <div className="container mx-auto px-4">
      <div className="flex flex-col items-center justify-center min-h-[calc(100vh-8rem)] text-center">
        <div className="flex items-center justify-center h-24 w-24 rounded-full bg-primary/10 mb-6">
          <Package className="h-12 w-12 text-primary" />
        </div>
        
        <h1 className="text-6xl font-bold mb-4">404</h1>
        <h2 className="text-2xl font-semibold mb-3 text-balance">Page Not Found</h2>
        <p className="text-muted-foreground text-lg mb-8 max-w-md text-pretty">
          The page you're looking for doesn't exist or has been moved.
        </p>
        
        <Button asChild size="lg">
          <Link href="/dashboard" className="flex items-center gap-2">
            <Home className="h-4 w-4" />
            Return to Dashboard
          </Link>
        </Button>
      </div>
    </div>
  )
}
