const BackgroundSvg: React.FC = () => {
  return (
    <svg xmlns='http://www.w3.org/2000/svg' className="fixed"  viewBox='0 0 2000 1500'>
      <rect fill='#000000' width='2000' height='1500'/>
      <defs>
        <ellipse fill='none' strokeWidth='1.6' strokeOpacity='0.67' id='a' rx='600' ry='450'/>
      </defs>
      <g transform='scale(0.919)' style={{ transformOrigin: 'center' }}>
        <g transform='' style={{ transformOrigin: 'center' }}>
          <g transform='rotate(-160 0 0)' style={{ transformOrigin: 'center' }}>
            <g transform='translate(1000 750)'>
              <use stroke='#4A034D' href='#a' transform='rotate(-60 0 0) scale(0.4)'/>
              <use stroke='#4d044f' href='#a' transform='rotate(-50 0 0) scale(0.5)'/>
              <use stroke='#500551' href='#a' transform='rotate(-40 0 0) scale(0.6)'/>
              <use stroke='#530653' href='#a' transform='rotate(-30 0 0) scale(0.7)'/>
              <use stroke='#570755' href='#a' transform='rotate(-20 0 0) scale(0.8)'/>
              <use stroke='#5a0857' href='#a' transform='rotate(-10 0 0) scale(0.9)'/>
              <use stroke='#5d0a59' href='#a'/>
              <use stroke='#600b5b' href='#a' transform='rotate(10 0 0) scale(1.1)'/>
              <use stroke='#630c5d' href='#a' transform='rotate(20 0 0) scale(1.2)'/>
              <use stroke='#670e5e' href='#a' transform='rotate(30 0 0) scale(1.3)'/>
              <use stroke='#6a0f60' href='#a' transform='rotate(40 0 0) scale(1.4)'/>
              <use stroke='#6d1062' href='#a' transform='rotate(50 0 0) scale(1.5)'/>
              <use stroke='#711264' href='#a' transform='rotate(60 0 0) scale(1.6)'/>
              <use stroke='#741366' href='#a' transform='rotate(70 0 0) scale(1.7)'/>
              <use stroke='#771468' href='#a' transform='rotate(80 0 0) scale(1.8)'/>
              <use stroke='#7b166a' href='#a' transform='rotate(90 0 0) scale(1.9)'/>
              <use stroke='#7e176b' href='#a' transform='rotate(100 0 0) scale(2)'/>
              <use stroke='#82186d' href='#a' transform='rotate(110 0 0) scale(2.1)'/>
              <use stroke='#851a6f' href='#a' transform='rotate(120 0 0) scale(2.2)'/>
              <use stroke='#891b71' href='#a' transform='rotate(130 0 0) scale(2.3)'/>
              <use stroke='#8c1c73' href='#a' transform='rotate(140 0 0) scale(2.4)'/>
              <use stroke='#8f1e74' href='#a' transform='rotate(150 0 0) scale(2.5)'/>
              <use stroke='#931F76' href='#a' transform='rotate(160 0 0) scale(2.6)'/>
            </g>
          </g>
        </g>
      </g>
    </svg>
  );
};

export default BackgroundSvg;
