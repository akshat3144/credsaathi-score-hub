import { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { isAuthenticated, setAuth, getCurrentUser } from "@/services/auth";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";

const Index = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { toast } = useToast();

  useEffect(() => {
    const handleOAuthCallback = async () => {
      // Check if we have a token in URL (OAuth callback)
      const token = searchParams.get("token");
      const error = searchParams.get("error");

      if (error) {
        toast({
          variant: "destructive",
          title: "Authentication Failed",
          description: "Unable to authenticate with Google. Please try again.",
        });
        return;
      }

      if (token) {
        try {
          // Store token temporarily
          localStorage.setItem("credsaathi_token", token);

          // Fetch user details
          const user = await getCurrentUser();

          // Store user and redirect
          setAuth(token, user);

          toast({
            title: "Welcome!",
            description: `Successfully logged in as ${user.name}`,
          });

          navigate("/dashboard", { replace: true });
        } catch (error) {
          console.error("Auth error:", error);
          toast({
            variant: "destructive",
            title: "Authentication Error",
            description: "Failed to complete authentication.",
          });
        }
        return;
      }

      // Auto-redirect authenticated users to dashboard
      if (isAuthenticated()) {
        navigate("/dashboard", { replace: true });
      }
    };

    handleOAuthCallback();
  }, [navigate, searchParams, toast]);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-br from-background to-accent px-4">
      <div className="text-center">
        <img
          src="/logo.png"
          alt="CredSaathi Logo"
          className="mx-auto w-72 h-72 object-contain"
        />
        {/* <h1 className="mb-4 text-5xl font-bold text-primary">CredSaathi</h1> */}
        <p className="mb-8 text-xl text-muted-foreground">
          AI-powered credit scoring for the gig economy
        </p>
        <div className="flex gap-4 justify-center">
          <Button size="lg" onClick={() => navigate("/login")}>
            Get Started
          </Button>
          <Button
            size="lg"
            variant="outline"
            onClick={() => navigate("/login")}
          >
            Sign In
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Index;
