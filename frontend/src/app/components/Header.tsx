"use client";

import React from 'react';
import { Button, Link, Navbar, NavbarBrand, NavbarContent, NavbarItem, Tab, Tabs } from "@nextui-org/react";

const Header = () => {
  return (
    <Navbar>
      <NavbarBrand>
        <h1 className="text-2xl font-bold text-transparent bg-gradient-to-r from-blue-500 to-purple-700 bg-clip-text">
            Research Chain
        </h1>
      </NavbarBrand>
      <NavbarContent className="hidden sm:flex gap-4" justify="center">
        <NavbarItem isActive>
          <Link href="#" aria-current="page">
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
