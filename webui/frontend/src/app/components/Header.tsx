'use client'
import React from 'react';
import { Navbar, NavbarBrand, NavbarContent, NavbarItem } from "@nextui-org/react";
import { FaGithub } from "react-icons/fa";
import Link from 'next/link';
import { usePathname } from 'next/navigation'

const Header = () => {
  const pathName = usePathname()

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
        <NavbarItem className='p-2' isActive={pathName === "/" ? true : false}>
          <Link href="/" className={pathName === "/" ? "text-blue-500 font-normal" : ''}>
            Add task
          </Link>
        </NavbarItem>
        <NavbarItem isActive={pathName === "/crawl-history" ? true : false}>
          <Link href="/crawl-history" className={pathName === "/crawl-history" ? "text-blue-500 font-normal" : ''} >
            Crawl history
          </Link>
        </NavbarItem >
        <NavbarItem isActive={pathName === "/summarize-history" ? true : false}>
          <Link href="/summarize-history" className={pathName === "/summarize-history" ? "text-blue-500 font-normal" : ''}>
            Summarize history
          </Link>
        </NavbarItem>
      </NavbarContent>
    </Navbar>
  );
}


export default Header;
