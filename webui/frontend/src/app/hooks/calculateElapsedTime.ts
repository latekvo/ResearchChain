export function calculateElapsedTime(timestamp: number): string {
    const now = new Date().getTime();
    const diffInMilliseconds = now - timestamp * 1000;
    const diffInMinutes = Math.floor(diffInMilliseconds / (1000 * 60));

    if (diffInMinutes >= 1440) {
      const diffInDays = Math.floor(diffInMinutes / 1440);
      return `${diffInDays} Day${diffInDays > 1 ? 's' : ''} ago`;
    } else if (diffInMinutes >= 60) {
      const diffInHours = Math.floor(diffInMinutes / 60);
      return `${diffInHours} Hour${diffInHours > 1 ? 's' : ''} ago`;
    } else {
      return `${diffInMinutes} Minute${diffInMinutes > 1 ? 's' : ''} ago`;
    }
  }
