import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { User, Mail, Phone, TrendingUp } from 'lucide-react';

interface ApplicantCardProps {
  applicant: {
    id: string;
    name: string;
    email: string;
    phone?: string;
    credit_score?: number;
    risk_tier?: string;
    gig_data?: {
      platforms: string[];
      average_rating: number;
    };
  };
  onPredict: (id: string) => void;
  onViewDetails: (id: string) => void;
}

const ApplicantCard = ({ applicant, onPredict, onViewDetails }: ApplicantCardProps) => {
  const getRiskBadgeVariant = (tier?: string) => {
    switch (tier) {
      case 'low':
        return 'default';
      case 'medium':
        return 'secondary';
      case 'high':
        return 'destructive';
      case 'very_high':
        return 'destructive';
      default:
        return 'outline';
    }
  };

  const getRiskLabel = (tier?: string) => {
    if (!tier) return 'Not Scored';
    return tier.replace('_', ' ').toUpperCase();
  };

  return (
    <Card className="hover:shadow-lg transition-shadow">
      <CardHeader>
        <div className="flex items-start justify-between">
          <div>
            <CardTitle className="flex items-center gap-2">
              <User className="h-5 w-5 text-muted-foreground" />
              {applicant.name}
            </CardTitle>
            {applicant.credit_score && (
              <div className="mt-2 flex items-center gap-2">
                <span className="text-2xl font-bold text-primary">{applicant.credit_score}</span>
                <Badge variant={getRiskBadgeVariant(applicant.risk_tier)}>
                  {getRiskLabel(applicant.risk_tier)}
                </Badge>
              </div>
            )}
          </div>
          {applicant.gig_data && (
            <div className="text-right">
              <div className="text-sm text-muted-foreground">Avg Rating</div>
              <div className="text-lg font-semibold">{applicant.gig_data.average_rating.toFixed(1)} ⭐</div>
            </div>
          )}
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Mail className="h-4 w-4" />
            {applicant.email}
          </div>
          {applicant.phone && (
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Phone className="h-4 w-4" />
              {applicant.phone}
            </div>
          )}
          {applicant.gig_data && applicant.gig_data.platforms.length > 0 && (
            <div className="mt-2 flex flex-wrap gap-1">
              {applicant.gig_data.platforms.slice(0, 3).map((platform) => (
                <Badge key={platform} variant="outline" className="text-xs">
                  {platform}
                </Badge>
              ))}
              {applicant.gig_data.platforms.length > 3 && (
                <Badge variant="outline" className="text-xs">
                  +{applicant.gig_data.platforms.length - 3}
                </Badge>
              )}
            </div>
          )}
        </div>
        <div className="mt-4 flex gap-2">
          <Button onClick={() => onPredict(applicant.id)} size="sm" className="flex-1">
            <TrendingUp className="mr-2 h-4 w-4" />
            Calculate Score
          </Button>
          <Button onClick={() => onViewDetails(applicant.id)} variant="outline" size="sm">
            View Details
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default ApplicantCard;
