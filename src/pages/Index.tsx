import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { isAuthenticated } from '@/services/auth';
import { Button } from '@/components/ui/button';

const Index = () => {
  const navigate = useNavigate();

  useEffect(() => {
    // Auto-redirect authenticated users to dashboard
    if (isAuthenticated()) {
      navigate('/dashboard', { replace: true });
    }
  }, [navigate]);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-br from-background to-accent px-4">
      <div className="text-center">
        <h1 className="mb-4 text-5xl font-bold text-primary">CredSaathi</h1>
        <p className="mb-8 text-xl text-muted-foreground">
          AI-powered credit scoring for the gig economy
        </p>
        <div className="flex gap-4 justify-center">
          <Button size="lg" onClick={() => navigate('/login')}>
            Get Started
          </Button>
          <Button size="lg" variant="outline" onClick={() => navigate('/login')}>
            Sign In
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Index;
