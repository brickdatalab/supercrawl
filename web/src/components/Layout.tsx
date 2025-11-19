import { Link, Outlet } from 'react-router-dom';

const Layout = () => {
    return (
        <div className="flex h-screen bg-background text-foreground">
            {/* Sidebar */}
            <aside className="w-64 border-r bg-card">
                <div className="p-6">
                    <h1 className="text-2xl font-bold text-primary">SuperCrawl</h1>
                </div>
                <nav className="mt-6 px-4 space-y-2">
                    <Link to="/" className="block px-4 py-2 rounded-md hover:bg-accent hover:text-accent-foreground">
                        Dashboard
                    </Link>
                    <Link to="/projects" className="block px-4 py-2 rounded-md hover:bg-accent hover:text-accent-foreground">
                        Projects
                    </Link>
                    <Link to="/chat" className="block px-4 py-2 rounded-md hover:bg-accent hover:text-accent-foreground">
                        AI Chat
                    </Link>
                    <Link to="/settings" className="block px-4 py-2 rounded-md hover:bg-accent hover:text-accent-foreground">
                        Settings
                    </Link>
                </nav>
            </aside>

            {/* Main Content */}
            <main className="flex-1 overflow-y-auto">
                <header className="h-16 border-b flex items-center px-8 bg-card">
                    <h2 className="text-lg font-medium">Dashboard</h2>
                    <div className="ml-auto">
                        {/* User Menu Placeholder */}
                        <div className="w-8 h-8 rounded-full bg-primary"></div>
                    </div>
                </header>
                <div className="p-8">
                    <Outlet />
                </div>
            </main>
        </div>
    );
};

export default Layout;
