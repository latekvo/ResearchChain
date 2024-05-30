import React from 'react';
import { Link, Navbar, NavbarBrand, NavbarContent, NavbarItem } from "@nextui-org/react";
import { FaGithub } from "react-icons/fa";


const Header = () => {
  return (
    <Navbar>
      <NavbarBrand>
        <h1 className="text-2xl font-bold text-transparent bg-gradient-to-r from-blue-500 to-purple-700 bg-clip-text">
            Research Chain
        </h1>
        <a href='https://github.com/latekvo/ResearchChain' target="_blank">
          <FaGithub className='ml-10 cursor-pointer' size="25"/>
        </a>
      </NavbarBrand>
      <NavbarContent className="hidden sm:flex gap-4" justify="center">
        <NavbarItem isActive>
          <Link href="#" aria-current="page" className='text-blue-500'>
            Add task
          </Link>
        </NavbarItem>
        <NavbarItem >
          <Link color="foreground" href="#">
            Crawl history
          </Link>
        </NavbarItem>
        <NavbarItem>
          <Link color="foreground" href="#">
            Summarize history
          </Link>
        </NavbarItem>
      </NavbarContent>
    </Navbar>
  );
}


export default Header;
